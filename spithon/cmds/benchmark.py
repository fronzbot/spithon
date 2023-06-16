"""Miscellaneous IC functions."""
import time
from statistics import mean
import click
from spithon.cmds.common import CONTEXT_SETTINGS
from spithon.core import spi


@click.group()
def benchmark():
    """Benchmarking commands."""
    pass


@benchmark.command(context_settings=CONTEXT_SETTINGS)
def spi_rd_wr():
    """Run multiple SPI writes and reads to benchmark durations."""
    num_ops = 2000
    write_times = []
    read_times = []
    start = time.time()
    spi.spi_write(0)
    end = time.time()
    print(f"Initial Write Operation = {(end-start)*1000} ms")

    iterations = range(0, num_ops)

    with click.progressbar(
        iterations, length=num_ops, label="Benchmarking SPI Writes."
    ) as pbar:
        for index in pbar:
            start = time.time()
            spi.spi_write(0)
            end = time.time()
            bench = (end - start) * 1000
            write_times.append(bench)
            time.sleep(0.01)

    with click.progressbar(
        iterations, length=num_ops, label="Benchmarking SPI Reads."
    ) as pbar:
        for index in pbar:
            start = time.time()
            spi.spi_read(0)
            end = time.time()
            bench = (end - start) * 1000
            read_times.append(bench)
            time.sleep(0.01)

    wr_max = round(max(write_times), 3)
    wr_min = round(min(write_times), 3)
    wr_avg = round(mean(write_times), 3)

    rd_max = round(max(read_times), 3)
    rd_min = round(min(read_times), 3)
    rd_avg = round(mean(read_times), 3)

    print("")
    print("RESULTS SUMMARY")
    print("-------------------")
    print(f"WRITES: Min = {wr_min} ms, Max = {wr_max} ms, Avg = {wr_avg} ms")
    print(f"READS:  Min = {rd_min} ms, Max = {rd_max} ms, Avg = {rd_avg} ms")
    print("")
