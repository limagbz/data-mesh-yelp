FROM ubuntu:22.04
ARG PYENV_VERSION=2.3.18
ARG POETRY_VERSION=1.5.1
ARG PYTHON_VERSION=3.11.3
ARG KUBECTL_VERSION=1.27.2
ARG KUBECTX_VERSION=0.9.4
ARG KUBENS_VERSION=0.9.4
ARG K9S_VERSION=0.27.4
ARG HELM_VERSION=3.12.0
ENV DEBIAN_FRONTEND=noninteractive

# Copy custom scripts and set the required permissions
COPY custom-scripts/ /tmp/scripts/
RUN chmod +x /tmp/scripts/*

# Required packages
RUN apt update && apt install -y git curl ca-certificates curl gnupg lsb-release locales locales-all nano

# Setting Locales
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install ZShell and OhMyZSH
RUN apt update && apt install -y zsh fonts-powerline fzf \
    && sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && chsh -s $(which zsh)

# Install Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt update && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Kubectl
RUN curl -fSsL -o /tmp/kubectl https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl \
    && mv /tmp/kubectl /bin/kubectl \
    && chmod +x /bin/kubectl

# Install Kubectx
RUN curl -fSsL -o /tmp/kubectx.tar.gz https://github.com/ahmetb/kubectx/releases/download/v${KUBECTX_VERSION}/kubectx_v${KUBECTX_VERSION}_linux_x86_64.tar.gz \
    && tar -C /tmp -xzf /tmp/kubectx.tar.gz && mv /tmp/kubectx /bin/kubectx \
    && chmod +x /bin/kubectx

# Install Kubens
RUN curl -fSsL -o /tmp/kubens.tar.gz https://github.com/ahmetb/kubectx/releases/download/v${KUBENS_VERSION}/kubens_v${KUBENS_VERSION}_linux_x86_64.tar.gz \
    && tar -C /tmp -xzf /tmp/kubens.tar.gz && mv /tmp/kubens /bin/kubens \
    && chmod +x /bin/kubens

# Install k9s
RUN curl -fSsL -o /tmp/k9s.tar.gz https://github.com/derailed/k9s/releases/download/v${K9S_VERSION}/k9s_Linux_amd64.tar.gz \
    && cd /tmp && tar -xvzf /tmp/k9s.tar.gz k9s && mv k9s /usr/local/bin/

# Install Pyenv and Python
ENV PYENV_ROOT="/usr/local/pyenv" PYENV_GIT_TAG=v${PYENV_VERSION}
ENV PATH="${PATH}:${PYENV_ROOT}/bin"
RUN apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    && curl https://pyenv.run | bash \
    && pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION}

# Install Poetry
RUN unset PYENV_VERSION && pyenv exec pip install poetry==${POETRY_VERSION}

# Install Helm
RUN curl -fSsL -o /tmp/helm.tar.gz https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
    && cd /tmp && tar -xvzf /tmp/helm.tar.gz linux-amd64/helm && mv linux-amd64/helm /usr/local/bin/
