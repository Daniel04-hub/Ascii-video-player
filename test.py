for r in range(0, 255, 40):
    for g in range(0, 255, 40):
        for b in range(0, 255, 40):
            print(f"\033[38;2;{r};{g};{b}m█\033[0m", end="")
    print()
