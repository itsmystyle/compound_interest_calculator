import argparse


def payout(cash, rate):
    return cash * rate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compound Interest Calculator.")
    parser.add_argument("initial_cash", type=float, help="Initial invested cash.")
    parser.add_argument("-apm", "--addition_per_month", type=float, default=0.0, help="Addition cash per month.")
    parser.add_argument("-ad", "--addition_duration", type=int, default=24, help="Addition cash duration (cycle).")
    parser.add_argument(
        "-pr", "--payout_rate", type=float, default=7.2, help="Pay out rate, e.g 7.2 for 7.2%%."
    )
    parser.add_argument(
        "-tic",
        "--total_invested_cash",
        type=float,
        help="Total invested cash. (termination criteria)",
    )
    parser.add_argument(
        "-gpc",
        "--generate_per_cycle",
        type=float,
        help="Generated cash per cycle. (termination criteria)",
    )
    parser.add_argument("-c", "--cycle", type=int, help="Cycles. (termination criteria)")
    parser.add_argument("-m", "--min_reinvest", type=float, default=1000.0, help="Minimum step up cash.")
    parser.add_argument("-v", "--verbose", type=int, default=0, help="Verbose.")

    args = parser.parse_args()

    if args.total_invested_cash is None and args.generate_per_cycle is None and args.cycle is None:
        raise Exception("Termination criteria is not given. Please use -h for more information.")

    accumulated_cash = args.initial_cash
    total_invested_cash = args.initial_cash
    leftout_cash = 0.0
    cycles = 0
    payout_cash = 0.0
    payout_rate = args.payout_rate / 100.0
    addition_duration = args.addition_duration

    while True:
        payout_cash = payout(accumulated_cash, payout_rate)
        leftout_cash += payout_cash
        if addition_duration > 0:
            addition_duration -= 1
            leftout_cash += args.addition_per_month
            total_invested_cash += args.addition_per_month
        multiply = leftout_cash // args.min_reinvest
        if multiply >= (1000/args.min_reinvest):
            accumulated_cash += multiply * args.min_reinvest
            leftout_cash %= args.min_reinvest
        cycles += 1

        if args.verbose > 0:
            print(f"Number of cycles: {cycles}")
            print(f"My invested cash: {total_invested_cash}")
            print(f"Invested cash: {accumulated_cash}")
            print(f"Cash generated in current cycle: {payout_cash}")
            print(f"ROI rate: {payout_rate}")
            print(f"Left out cash: {leftout_cash}")
            print("======================================================")

        if args.total_invested_cash is not None and accumulated_cash >= args.total_invested_cash:
            break
        if args.cycle is not None and cycles >= args.cycle:
            break
        if args.generate_per_cycle is not None and payout_cash >= args.generate_per_cycle:
            break

    print("Initial invested cash: {}".format(args.initial_cash))
    print("My total invested cash: {}".format(total_invested_cash))
    print("Invested cycles: {}".format(cycles))
    print("Total invested cash: {}".format(accumulated_cash))
    print("Generated cash per cycle: {}".format(payout_cash))
