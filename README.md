![](https://img.shields.io/badge/<Implementation>-<active_contour_corteximage>-<success>)
![](https://img.shields.io/badge/<Implementation>-<real-time-recognition/alarm>-<success>)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R5R11K2H4)
# General Idea/ Modifications


## Getting Started

Simply open the jupyter notebook and see how some demo on pictures that we uploaded with this repository

### Prerequisites

What things you need to install the software and how to install them

```
scikit-image
matplotlib
numpy
notebook
scipy
```

### Installing

Here are the steps to follow

#### Usual way
Installing using requirements.txt
```
pip3 install -r requirements.txt
```

#### Docker way
Installing using docker (if you have it installed it can make sure there is no problem linked to packages in the whole process)
```
docker build -t <docker-name> .
docker run -it --ipc=host -p 9999 <docker-name> 
```


Obviously you are free to add any options, here I added 9999 port in case you want to access with a jupyter notebook, and --ipc=host in case you want to train for new models of darknet itself (though we do not support this)

## Running the tests


### Break down into end to end tests


## Deployment

None yet, you can do some pull requests to me

## Built With

* [python3](https://www.python.org/download/releases/3.0/) - The web framework used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors
Michael Chan
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments









