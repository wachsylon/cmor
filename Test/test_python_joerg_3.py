from __future__ import print_function
import cmor
import numpy

ntimes = 1
nlat = 45
nlon = 90
nlev = 5


def prep(mode):
    error_flag = cmor.setup(
        inpath='Tables',
        netcdf_file_action=mode)

    error_flag = cmor.dataset_json("Test/CMOR_input_example.json")


def prep_var(var, units):
    # creates 1 degree grid
    dlat = 180 / nlat
    dlon = 360. / nlon
    alats = numpy.arange(-90 + dlat / 2., 90, dlat)
    bnds_lat = numpy.arange(-90, 90 + dlat, dlat)
    alons = numpy.arange(0 + dlon / 2., 360., dlon) - 180.
    bnds_lon = numpy.arange(0, 360. + dlon, dlon) - 180.
    cmor.load_table("Tables/CMIP6_6hrLev.json")
    # cmor.load_table("Test/IPCC_table_A1")
    ilat = cmor.axis(
        table_entry='latitude',
        units='degrees_north',
        length=nlat,
        coord_vals=alats,
        cell_bounds=bnds_lat)

    ilon = cmor.axis(
        table_entry='longitude',
        length=nlon,
        units='degrees_east',
        coord_vals=alons,
        cell_bounds=bnds_lon)

    zlevs = numpy.zeros(5, dtype='d')
    zlevs[0] = 0.1999999999999999999
    zlevs[1] = 0.3
    zlevs[2] = 0.55
    zlevs[3] = 0.7
    zlevs[4] = 0.99999999

    zlev_bnds = numpy.zeros(6, dtype='d')
    zlev_bnds[0] = 0.
    zlev_bnds[1] = 0.2
    zlev_bnds[2] = 0.42
    zlev_bnds[3] = 0.62
    zlev_bnds[4] = 0.8
    zlev_bnds[5] = 1.

    itim = cmor.axis(
        table_entry='time1',
        units='days since 2010-1-1')

    ilev = cmor.axis(
        table_entry="alternate_hybrid_sigma",
        units='1',
        coord_vals=zlevs,
        cell_bounds=zlev_bnds)

    p0 = numpy.array([1.e5, ])
    a_coeff = numpy.array([0.1, 0.2, 0.3, 0.22, 0.1])
    b_coeff = numpy.array([0.0, 0.1, 0.2, 0.5, 0.8])
    a_coeff_bnds = numpy.array([0., .15, .25, .25, .16, 0.])
    b_coeff_bnds = numpy.array([0., .05, .15, .35, .65, 1.])

    ierr = cmor.zfactor(zaxis_id=ilev,
                        zfactor_name='ap',
                        units='Pa',
                        axis_ids=[ilev, ],
                        zfactor_values=a_coeff,
                        zfactor_bounds=a_coeff_bnds)

    ierr = cmor.zfactor(zaxis_id=ilev,
                        zfactor_name='b',
                        axis_ids=[ilev, ],
                        zfactor_values=b_coeff,
                        zfactor_bounds=b_coeff_bnds)

    # ierr = cmor.zfactor(zaxis_id=ilev,
    # zfactor_name='p0',
    # units='Pa',
    # zfactor_values=p0)

    ips = cmor.zfactor(zaxis_id=ilev,
                       zfactor_name='ps1',
                       axis_ids=[itim, ilat, ilon],
                       units='Pa')

    ivar1 = cmor.variable(
        var,
        axis_ids=[
            itim,
            ilev,
            ilat,
            ilon],
        units=units,
        missing_value=0.)
    return ivar1, ips


for d in range(2):
    mode = cmor.CMOR_APPEND
    if d == 0:
        mode = cmor.CMOR_REPLACE
    prep(mode)
    ivar1, ips1 = prep_var("ta", "K")
    ivar2, ips2 = prep_var("hus", "%")
    for i in range(4):
        tval = [i / 4. + d]
        tbnd = [i / 4. + d - 0.125, i / 4. + d + 0.125]
        print('tvar', tval)
        print('tbnd', tbnd)
        print('writing time:', i, i / 4.)
        data = numpy.random.random((ntimes, nlev, nlat, nlon)) * 30. + 273
        data = data.astype("f")
        cmor.write(ivar1, data, time_vals=tval, time_bnds=tbnd)
        print('wrote var 1 time:', i)
        data = numpy.random.random((ntimes, nlev, nlat, nlon))
        data = data.astype("f")
        cmor.write(ivar2, data, time_vals=tval, time_bnds=tbnd)
        print('wrote var 2 time:', i)
        data = numpy.random.random((ntimes, nlat, nlon)) * 8. + 96300.
        data = data.astype("f")
        cmor.write(
            ips1,
            data,
            store_with=ivar1,
            ntimes_passed=1,
            time_vals=tval,
            time_bnds=tbnd)
        print('wrote ps in var 1 time:', i)
        cmor.write(
            ips2,
            data,
            store_with=ivar2,
            ntimes_passed=1,
            time_vals=tval,
            time_bnds=tbnd)
        print('wrote ps in var 2 time:', i)
    file1 = cmor.close(ivar1, True)
    file2 = cmor.close(ivar2, True)
    print('File1:', file1)
    print('File2:', file2)
    cmor.close()
