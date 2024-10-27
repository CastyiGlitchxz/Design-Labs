[![ESLint](https://github.com/CastyiGlitchxz/Design-Labs/actions/workflows/eslint.yml/badge.svg?branch=main)](https://github.com/CastyiGlitchxz/Design-Labs/actions/workflows/eslint.yml)
# How to use Design Labs

 To use Design Labs you first need to open your a terminal on your computer and cd to the location of server.py
 Then run "Python3 server.py" for macOS
 or "Python server.py" for Windows and Linux to run the server

 Then go to http://127.0.0.1:8000
 There you go you have Design Labs running

# How to load Labs

 First go to /design/base.html
 base.html is the base of your lab and is responsible for displaying your work
 On your ide or file browser you should see a labs folder open it then create a new folder with the name of your lab and inside that file make a html file you can name it whatever you want
## (ex: 'example_lab' inside that folder 'render.html')
 To load your lab go back to base.html and you should see a line of text that looks like 
## <span style="color:red">{% extends '/labs/example_lab/render.html' %}</span> change that to <span style="color:green">{% extends '/labs/your_labs_name/your_render_file.html' %}</span>
 I know not thw most efficient way to load a lab, I'll come up with a better solution one day

# What your files should look like

## Inside your render file
### The inside of your render file should like
```html

<main>

</main>

```
or
```html

<!-- This is the main designer for design labs -->
<!-- Insert html in the "main" tag to test -->

<main>
    <container class="grid_container">
        <h1 class="custom_design_labs_header_text_h1">Example Lab</h1>
        <container class="flex_container">
            <button class="custom_design_labs_button">Continue</button>
            <button class="custom_design_labs_button">Restart</button>
            <button class="custom_design_labs_button">Start Designing</button>
        </container>

        <input class="custom_design_labs_input" type="text" placeholder="Example Input"/>
    </container>
</main>

<!-- Do not, I repeat do not put in !Doctype it will break the code -->
<!-- Save this file to apply changes -->

 ```

You put your main code inside the the ```<main></main>``` tags like the example above
