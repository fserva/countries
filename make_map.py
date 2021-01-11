import numpy as np
#import matplotlib.pyplot as plt
import countries
import netCDF4 as nc4

cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')

# Parameters used for the output file
version = '0.1'
dlon = 0.1 
dlat = dlon

lons = np.linspace(-180,180,int((360/dlon)+1))
lats = np.linspace( -90, 90,int((180/dlat)+1))

country_codes = []

counter = 0.

# Get all countries code to associate integer. Number of 
# countries is between 190 and 250 depending on the convention.
for il in range(len(lons)):
    for jl in range(len(lats)):

        country_code = cc.getCountry(countries.Point(lats[jl], lons[il]))

        if country_code is not None and country_code.iso not in country_codes:
            country_codes.append(country_code.iso)

        print(counter/(len(lons)*len(lats))) 
        counter += 1


# Add non-existent code to start count from 1. Sea/inland waters are = 0.
country_codes = ['ZZ']+country_codes

ncountries = len(country_codes)

country_codes = np.array(country_codes)

country_vals = np.zeros((len(lats),len(lons)))

for il in range(len(lats)):
    for jl in range(len(lons)):

        country_code = cc.getCountry(countries.Point(lats[il], lons[jl]))

        if country_code is not None:
            country_num = np.where(country_codes==country_code.iso)[0][0]
            country_vals[il,jl] = country_num 


"""
plt.figure()
levels = 1+np.arange(ncountries)
plt.contourf(lons,lats,country_vals.T,levels=levels)

plt.show()
"""

# Save output file with proper name
ncout = nc4.Dataset('./countries_gridded_'+str(dlon)+'deg_v'+version+'.nc','w')

ncout.createDimension('lat',len(lats))
ncout.createDimension('lon',len(lons))
ncout.createDimension('iso',ncountries)

latss = ncout.createVariable('lat',float,('lat'))
lonss = ncout.createVariable('lon',float,('lon'))
ctrss = ncout.createVariable('iso',str,('iso'))
ctrms = ncout.createVariable('country',int,('lat','lon'))

latss[:] = lats
latss.units = 'degrees_north'
latss.standard_name = 'latitude'
latss.axis = 'Y'

lonss[:] = lons
lonss.units = 'degrees_east'
lonss.standard_name = 'longitude'
lonss.axis = 'X'

ctrss[:] = country_codes
ctrss.units = 'ISO code'

ctrms[:] = country_vals
ctrms.comment = 'Use iso to get number-country correspondence'

ncout.close()
