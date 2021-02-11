# IvanZuev_EPAM_final_task

To start project you should without arguments you should have:
1) 'Hotels.zip' in 'input_data' storage
2) 'openweathermap_appid.json' in 'input_data' storage

So, you can run:
~~~
python main.py
~~~

###Input data

If you don't have 'Hotels.zip' in 'input_data' storage, you can send your oun file. Use:
~~~
python main.py --input_file {path to your file}
~~~

###appid
If you don't have 'openweathermap_appid.json' in 'input_data' storage, you can add your oun appid. Use:

~~~
python main.py --appid {your appid}
~~~

If you have your oun file with some appid you can use add it by:
~~~
python main.py --appidpath {your file with appid}
~~~
This file should be JSON and contains appid in the next format:
~~~
{'appid': {} }
~~~
### Output data

You also can specify output_folder where all data will be saved.

Use:
~~~
python main.py --outdir {your output folder}
~~~





### Threads
Also you can specify max number of threads. Use:
~~~
python main.py --threads {max number of threads}
~~~
Default number of threads is 64.
