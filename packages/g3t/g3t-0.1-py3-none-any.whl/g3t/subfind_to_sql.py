#!/usr/bin/python
import pp
from pp_schema  import *
import g3read as g
import numpy as np
import sys
import logging
import numpy as np
import argparse

"""
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
"""

def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)




        
def dtl(DL,n, cols=None):
    keys = DL.keys()
    return [{key: DL[key][i] for key in keys if len(DL[key])>i and (cols is None or key in cols)} for i in range(n)]
def ltd(LD):
    return {k: [dic[k] for dic in LD] for k in LD[0]}

def flat_props(props,n, cols=None):

        i = [x for x in props.items()]
        
        for prop,oldprop in i:
            if len(props[prop].shape)>1:
                del  props[prop]
                #print(prop, cols)
                for i_in_prop in range(oldprop.shape[1]):
                    #print(i_in_prop)
                    if cols is not None and prop+str(i_in_prop) in cols:
                        props[prop+str(i_in_prop)]=oldprop[:,i_in_prop]
                    elif cols is None: 
                        props[prop+str(i_in_prop)]=oldprop[:,i_in_prop]
        lprops = dtl(props,n,cols)
        return lprops
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value yes/true/t/y/1/no/false/f/n/0 expected. Got:%s '%v)

def main():
    import numpy as np
    import json
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--basename', type=str, help='base file name of groups', required=True)
    parser.add_argument('--simulation-name', type=str,help='name of simulation', required=True)
    parser.add_argument('--tag', type=str,help='tag for snapshot', required=True)
    parser.add_argument('--snap', type=str,help='snap___', required=True)

    parser.add_argument('--min-field', type=str, default="GLEN")
    parser.add_argument('--min-val', type=float, default=0.)


    parser.add_argument('--add-fof', type=str2bool, default=True)


    parser.add_argument('--add-sf-bounds', type=str2bool, default=False)

    parser.add_argument('--add-sf-data', type=str2bool, default=False)


    parser.add_argument('--look', type=str, default="MCRI")
    parser.add_argument('--only-subfind-existing-columns', action='store_true', default=False)
    parser.add_argument('--only-fof-existing-columns', action='store_true', default=False)

    parser.add_argument('--format', type=str, default="%e")
    parser.add_argument('--delete-groups', help="delete all fofs of the snap before inserting. If false, tries to edit them", type=bool, default=False)
    args = parser.parse_args()
    for k in args.__dict__:
        print(k,args.__dict__[k])

    args.first_file = 0
    basegroup = args.basename+'groups_%s/sub_%s.'%(args.snap,args.snap)
    first_filename = basegroup+'0'
    first_file = g.GadgetFile(first_filename, is_snap=False)


    header = first_file.header
    nfiles = header.num_files        
    redshift = header.redshift
    a = 1./(1.+redshift)

    #get FOF and SF blocks
    FOF_blocks=[]
    SF_blocks=[]

    all_blocks = first_file.blocks
    for block_name in all_blocks:
        ptypes = all_blocks[block_name].ptypes
        if ptypes[0]: FOF_blocks.append(block_name)
        if ptypes[1]: SF_blocks.append(block_name)

    simulation = Simulation.get_or_none(name=args.simulation_name)
    if simulation is None:
        simulation = Simulation(name = args.simulation_name, box_size=header.BoxSize, path=args.basename, h=header.HubbleParam)
        simulation.save()
    
    
    snap = simulation.snaps.where(Snap.name==args.snap).first()
    new_snap = False
    if snap is None:
        snap = Snap(simulation=simulation, name=args.snap, redshift=redshift, a =a, tag=args.tag)
        new_snap=True
        snap.save()
    elif args.add_fof and not args.delete_groups:
        test_fof = FoF.select().where((FoF.snap==snap) & (FoF.resolvness==1)).first()
        if test_fof!=None:
                raise Exception("Clusters for this simulation and snapshot  already present in the databse :(")

    #print(args.add_fof, args.delete_groups, args.add_fof and not args.delete_groups)

    if args.delete_groups:
        fofs = snap.fofs
        Galaxy.delete().where(Galaxy.snap == snap). execute()
        FoF.delete().where(FoF.snap==snap).execute()
        FoFFile.delete().where(FoFFile.snap==snap).execute()

    max_fof_id = None
    if args.add_sf_bounds or args.add_sf_data:
        cluster = FoF.select().where((FoF.snap==snap) & (FoF.resolvness==1)).order_by(FoF.glen.asc()).first()
        if cluster is not None:
            max_fof_id = cluster.id_cluster
            args.min_val = 0
            printf("Max FoF ID: %d\n"%(max_fof_id))

    subfind_cols = None
    if args.only_subfind_existing_columns:
        subfind_cols = [f for f in Galaxy.__dict__ if f[0]!='_' and f!='DoesNotExist']
        printf("Subfind columns: %s\n"%( ' '.join(subfind_cols)),e=True)
    fof_cols = None
    if args.only_fof_existing_columns:
        fof_cols = [f for f in Galaxy.__dict__ if f[0]!='_' and f!='DoesNotExist']
        printf("FoF columns: %s\n"%( ' '.join(fof_cols)),e=True)
        

    ifof = 0
    previous_info = None
    for ifile in range(args.first_file,nfiles):
        filename = basegroup+str(ifile)
        f = g.GadgetFile(filename, is_snap=False)
        foffile = FoFFile.select().where((FoFFile.snap==snap)&(FoFFile.ifile==ifile)).first()
        if foffile is None:
            FoFFile.insert(snap=snap,id_first_cluster=ifof,ifile=ifile).execute()
        if f.info is None: 
            f.info = previous_info
        else:
            previous_info = f.info
        val = f.read_new(args.min_field,0)
        n_fof_groups = len(val)
        printf("FIlename: %s,  from id_cluster=%d %f < %f < %s < %f \n"%(filename,ifof,args.min_val,np.min(val),args.min_field,np.max(val)),e=True)
        if (args.add_fof and np.max(val)<args.min_val):
            printf("Reached min val\n");
            break
        if args.add_fof: #insert FOFs
            props={}
            for FOF_block in FOF_blocks :

                props[FOF_block.lower().replace(" ", "")] = f.read_new(FOF_block,0)
            props["id_cluster"] = np.arange(n_fof_groups)+ifof
            props["i_file"] = np.zeros(n_fof_groups)+ifile
            props["i_in_file"] = np.arange(n_fof_groups)
            props["snap_id"] =     np.zeros(n_fof_groups)+snap.id

            props["start_subfind_file"] = np.zeros(n_fof_groups)-1
            props["end_subfind_file"] = np.zeros(n_fof_groups)-1
            props["resolvness"] = np.zeros(n_fof_groups)+1
            
            lprops  = flat_props(props, n_fof_groups, fof_cols)
            #print (props,lprops)
            printf("Clusters: len=%d N=%d from %d to %d\n"%(len(lprops), n_fof_groups,ifof, ifof+n_fof_groups))
            ifof+=n_fof_groups
            param = args.look.lower().replace(" ", "")
            s= "Block: %%s, min=%s; max=%s \n"%(args.format,args.format)
            printf(s%(param,np.min(props[param]), np.max(props[param])))
            n_inserts = 0
            with db.atomic():
                n_insert_per_chunk=15
                for idx in range(0, len(lprops)+ n_insert_per_chunk, n_insert_per_chunk):
                    chunk = lprops[idx:idx + n_insert_per_chunk]
                    #print(chunk)

                    if len(chunk)>0:
                        FoF.insert_many(chunk).execute()
                    n_inserts+=len(chunk)
            printf("Clusters: %d inserted\n"%(n_inserts))

        if args.add_sf_bounds or args.add_sf_data:
            grnrs = f.read_new("GRNR",1)
            if (max_fof_id is not None and np.min(grnrs)>max_fof_id):
                printf("Reached max fof %d\n"%max_fof_id);
                break
            ufofs = np.unique(grnrs)
            fof_ids_in_sf = ufofs.tolist()

        if args.add_sf_bounds:
            q1 = """update FoF set end_subfind_file = {ifile:d} where snap_id={snap_id:d} and id_cluster in ({inc:s});\n""" .format(ifile=ifile, snap_id=snap.id, inc=','.join(map(str, fof_ids_in_sf)))
            q2 = """update FoF set start_subfind_file = {ifile:d} where snap_id={snap_id:d} and id_cluster in ({inc:s}) and start_subfind_file=-1;\n""" .format(ifile=ifile, snap_id=snap.id, inc=','.join(map(str, fof_ids_in_sf)))
            n1 = db.execute_sql(q1)
            n2 = db.execute_sql(q2)
            n_inserts = len(fof_ids_in_sf)
            printf("Updated bounds of (max) %d clusters.\n"%(n_inserts))

        if args.add_sf_data: #insert SFs
            props={}
            mask = np.in1d(grnrs,ufofs)
            for SF_block in SF_blocks :
                props[SF_block.lower().replace(" ", "")] = f.read_new(SF_block,1)[mask]
            props["id_cluster"] = props["grnr"]
            nsfs = len(props["grnr"])
            props["snap_id"] = np.zeros(nsfs)+snap.id
            props["i_file"] = np.zeros(nsfs)+ifile
            lprops  = flat_props(props, nsfs, subfind_cols)
            printf("Galaxies: N=%d/%d, from cluster %d to cluster %d\n"%(nsfs,len(grnrs), np.min(props["grnr"]), np.max(props["grnr"])))
            n_inserts = 0
            with db.atomic():
                n_insert_per_chunk=15
                for idx in range(0, len(lprops)+ n_insert_per_chunk, n_insert_per_chunk):
                    chunk = lprops[idx:idx + n_insert_per_chunk]
                    if len(chunk)>0:
                        Galaxy.insert_many(chunk).execute()
                    n_inserts+=len(chunk)
            printf("Galaxy: %d inserts \n"%(n_inserts))

        printf("\n")

if __name__ == "__main__": 
    main()
    sys.exit(0)
