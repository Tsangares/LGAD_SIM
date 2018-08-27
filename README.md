# What is this?
This simulates six detecting planes and can estimate the resolutions of a telescope tracker.

# Installation
Simply

    pip insatll lgad


# CLI

Run commands by typing in

    `lgad [type]`

Where type is one of the simulation to run. Currently type could be `single`, `sensor`, `thick` or `sizing`.

To find out the other arguments type in the commmand:

    lgad --help

The flag `-n` represets the number of events to run per simulation.

`single` runs one simulation with the specified configuation file and sensor parameters.

`--config location` will specify the location of a json config file.
An example of a plates config file is located in the `