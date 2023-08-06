# Migos !

Yet Another Static Site 

https://mardix.github.io/migos

---

Thank you for using Migos 

## Quickstart

### Create your site

You see this page because you've already created the site, so no need to create 
the site again, but for future reference, to create a (another) website, just go 
to the root of all your sites, and type the following 

```
migos create YOUR-SITE-NAME
cd YOUR-SITE-NAME
```

or you could just go into the directory you want to turn into a static site, and type the following:

```
migos init
```

It will setup everything in the current directory

### Developing & Serving

While developing, you will want to see the changes. Run the code below, it will 
allow you to see the changes you make, and will reload whenever you make a change.

```
migos serve
```

### Build your site

To build your site, run `build`. It will generate all the pages and place them 
inside of `/build` directory. The content in that directory can be published 
to where ever you like.

```
migos build 
```
    
### Publish your site

To publish your site, after `migos build`, upload the directory `/build` to 
your hosting providers.
    
### Clean the build directory

There is really no need to keep the generated files inside of the build. So
you can delete them. Because your still have your `/pages` and `/static` folder. 
You'll just have to `migos build` to have the content back in there.

```
migos clean
``` 
    
To learn more, go to https://mardix.github.io/migos
    
--- 

## Add-ons

Just for your convenience, we have included `milligram.css`

- https://github.com/milligram/milligram
    


