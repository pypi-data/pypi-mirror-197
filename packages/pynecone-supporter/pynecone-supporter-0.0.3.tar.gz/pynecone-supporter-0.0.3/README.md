# pynecone-supporter

https://pypi.org/project/pynecone-supporter
<pre>
pip install pynecone-supporter
</pre>

Install Node.js (npm) (Windows)  
https://nodejs.org/ko/download/  
https://nodejs.org/download/release/v13.9.0/  

Supported APIs
<pre>
import pynecone_supporter

pynecone_supporter.color_picker
pynecone_supporter.jumo_button
pynecone_supporter.json_editor
</pre>

app/pcconfig.py  
```
import pynecone as pc

config = pc.Config(
    app_name="my_app",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    frontend_packages=[ #
        "react-colorful", #
        "react-supporter", #
        "react-jsondata-editor" #
    ], #
)
```

Examples:  

https://github.com/automatethem/pynecone-supporter/blob/main/examples/color_picker/app/app/app.py  

https://github.com/automatethem/pynecone-supporter/blob/main/examples/jumo_button/app/app/app.py  

https://github.com/automatethem/pynecone-supporter/blob/main/examples/json_editor/app/app/app.py

<img src="https://github.com/automatethem/pynecone-supporter/blob/main/readme_files/screenshot1.PNG?raw=true">
