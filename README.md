# Conan graph3d generator:

This [Conan generator](https://docs.conan.io/en/latest/howtos/custom_generators.html) will generate a
html file with a 3d visualization for the dependency graph.

![Conan graph 3D](graph.png?raw=true)

# To install the generator:

``` bash
git clone https://github.com/czoido/conan-graph3d
cd conan-graph3d
conan config install graph3d.py -tf generators
```

Create your consumer project ([see docs](https://docs.conan.io/en/latest/getting_started.html)) with
a *conanfile.txt* like this:

```
[requires]
sdl/2.0.20
sdl_image/2.0.5
```

Then:

```
conan install . -g graph3d --build=missing
```


A *conan-graph3d.html* file is generated. Open to see the graph.
