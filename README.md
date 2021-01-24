# IvanZuev_EPAM_final_task

To start project you should run in terminal:

'python testing_file.py {input folder} {output folder}'


{input folder} should contains 'hotels.zip'

Also {input folder} can contais 'openweathermap_appid.json' with appids. You need appid to get weather from openweathermap.com.

If you don't have 'openweathermap_appid.json' you can add 'appid' manually. Use --appid to add it. 
After first run with this argument, 'openweathermap_appid.json' will be created.

Also you can set number of threads using '--threads'. Default number of threads is 4.