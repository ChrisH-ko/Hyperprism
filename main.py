from code.classes import chip
from code.visualization import visualize as vis

if __name__ == "__main__":
    chip_id = 0
    net_id = 1

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)

    print(test_chip)
    print(vis.visualize(test_chip))