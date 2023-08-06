# Introduction
`Endoscopie`는 OS 이미지로 생성된 Virtual Machine(이하 VM)의 기본 동작을 테스트하는 도구입니다.

> `endoscopie`는 내시경을 의미(endoscopy)하는 단어로 VM 내부를 들여다보고(?) 검사하는 도구


# Installation

## Requirements

- `python` >= 3.9, < 4.0
- `terraform`

## Install Terraform

### CentOS/RHEL

1. Install `yum-utils` package

```shell
$ sudo yum install -y yum-utils
```
2. Add yum repository

```shell
$ sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
```
3. Confirm repository is added

```shell
$ sudo dnf repolist
repo id       repo name
hashicorp     Hashicorp Stable - x86_64
```
4. Install `terraform`

```shell
$ sudo yum -y install terraform
```

### Ubuntu/Debian

1. You will use these packages to verify HashiCorp's GPG signature and install HashiCorp's Debian package repository.

```shell
$ sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
```
2. Install the HashCorp `GPG key`

```shell
$ wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
```
3. Verify the key's fingerprint

```shell
$ gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
```
4. Add the official HashiCorp repository to your system. 

```shell
$ echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
```
5. Download the package information from HashiCorp.

```shell
$ sudo apt update
```
6. Install Terraform from the new repository

```shell
$ sudo apt-get -y install terraform
```

### OS X
1. First, install the HashiCorp tap, a repository of all our Homebrew packages.

```shell
$ brew tap hashicorp/tap
```
2. Now, install Terraform with `hashicorp/tap/terraform`.

```shell
$ brew install hashicorp/tap/terraform
```
3. To update to the latest version of Terraform, first update Homebrew.

```shell
$ brew update
```
4. Then, run the `upgrade` command to download and use the latest Terraform version.

```shell
$ brew upgrade hashicorp/tap/terraform
```

## Verify the installation
Verify that the installation worked by opening a new terminal session and listing Terraform's available subcommands.

```shell
$ terraform --help
Usage: terraform [global options] <subcommand> [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands. 
...
```

## Install Endoscopie

```shell
$ pip install endoscopie==0.1.0
```


# Test Configuration
`endoscopie`로 테스트를 수행할 때, OS 이미지에 대한 정보와 더불어 VM이 생성된 후 의도한 대로 동작하고 있는지를 확인할 수 있는 정보들도 제공해야 합니다.
아래에 테스트 실행을 위한 필수 필드와 검증해야할 정보들을 보여주는 `.yaml` 파일 예시가 있습니다.

```yaml
openstack:
  OS_REGION_NAME: # region name (ex: kr-central-1)
  OS_AUTH_URL: # openstack auth url
  OS_AUTH_TYPE: # v3applicationcredential
  OS_APPLICATION_CREDENTIAL_ID: # openstack application credential id 
  OS_APPLICATION_CREDENTIAL_SECRET: # openstack application credential secret
bastionHost:
  ip: # Bastion host ip(v4) 
  user: # OS login username
  keypair:
    name: # keypair file name for bastion host
    path: # keypair file path for bastion host
instance:
  keypair:
    name: # keypair file name for new instances
    path: # keyapir file path for new instances
    description:
  vpc:
    id: # user vpc id
    subnet: # user vpc subnet id
    securityGroups:
      - # security groups
images:
  - id: # OS image id 
    name: # OS image name (ex: Ubuntu 18.04)
    osType: # type of os name (ex: ubuntu, centos, rocky, or almalinux)
    osVersion: # OS version
    osUser: # OS username (for login user)
    volumeSize: # root volume size (ex: 100) GiB
    flavors:
      - name: # flavor name
        id:  # flavor id
    userScript:
      path: 
    assertThat:
      resources:
        - vCPU: 
          memory: 
          volume: 
      processes:
        - # running processe(s)
      ports:
        - # opened port(s)
  ...
```

## Description
> 위에 예시로 제시된 필드 대부분은 필수 필드이며, 생각 가능한 경우 별도 표시

- `openstack`: 테스트 수행 환경의 사용자 인증 정보 설정
- `bastionHost`: 사설망에 생성되는 VM에 접속하기 위한 bastion host 정보 설정
- `instance`: 생성되는 VM에 공통적으로 적용되는 정보 설정
- `images`: 테스트할 이미지와 플레이버 정보, 생성된 VM 검사를 위한 조건 설정
  - `flavors` : 여러개의 플레이버 정보를 설정 가능
  - `assertThat.resources`: `flavors`에 설정한 개수와 순서대로 설정


# Usage

To get a list of basic options and switches use:

```shell
$ endoscopie --help

 Usage: endoscopie [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                                                         │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. [default: None]                                  │
│ --help                                                       Show this message and exit.                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ cleanup                                                                                                                                                                                          │
│ run                                                                                                                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command `run`

```shell
$ endoscopie run --help

 Usage: endoscopie run [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config        PATH  Set YAML file in which the datas required for image verify. [default: None] [required]                                                                                  │
│    --help                Show this message and exit.                                                                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Command `cleanup`

```shell
$ endoscopie cleanup --help

 Usage: endoscopie cleanup [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ 

```

