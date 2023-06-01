#!/usr/bin/env bash
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

echo -e "\n${YELLOW}Running Post Create Commands...${NC}"

echo -e "\n${BLUE}Installing Custom Theme ZSHELL...${NC}"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
