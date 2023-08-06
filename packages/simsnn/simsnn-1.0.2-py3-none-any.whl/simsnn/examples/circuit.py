from simsnn.core.networks import Network
from simsnn.core.simulators import Simulator


def run(duration=10, options=None):
    options = {} if options is None else options

    # Create the network and the simulator object
    net = Network()
    sim = Simulator(net)

    # Create a programmed neuron, that spikes on times 1 and 3,
    # does not repeat it's programming and has the ID "pn".
    programmed_neuron = net.createInputTrain(train=[0, 1, 0, 1], loop=False, ID="pn")

    # Create a LIF neuron, with a membrane voltage threshold of 1,
    # a post spike reset value of 0 and no voltage decay (m=1).
    lif_neuron = net.createLIF(ID="ln", thr=1, V_reset=0, m=1)

    # Create a Synapse, between the programmed neuron and the LIF neuron,
    # with a voltage weight of 1 and a delay of 1.
    net.createSynapse(pre=programmed_neuron, post=lif_neuron, ID="pn-ln", w=1, d=1)

    # Add all neurons to the raster
    sim.raster.addTarget([programmed_neuron, lif_neuron])
    # Add all neurons to the multimeter
    sim.multimeter.addTarget([programmed_neuron, lif_neuron])

    # Run the simulation for 10 rounds, enable the plotting of the raster,
    # the multimeter and the network structure.
    sim.run(duration, plotting=True, options=options)
