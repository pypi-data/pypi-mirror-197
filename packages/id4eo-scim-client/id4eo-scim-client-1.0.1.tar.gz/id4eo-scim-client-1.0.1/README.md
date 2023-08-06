<p align="center">
  <h3 align="center">id4eo_scim</h3>
  <p align="center">
    Auxiliary Python3 library that allows a client to dynamically register with Gluu and access SCIM endpoints to get/add/edit/remove user attributes
  </p>
</p>

## Table of Contents

- [Setup this template!](#setup-this-template)
- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Testing](#testing)
- [Documentation & Usage](#documentation--usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About The Project

This is an auxiliary Python3 library to allow a client to dynamically register with Gluu. At the same time, it allows to get all user attributes, and also add/edit/remove specific attributes, by using SCIM endpointsWith both OAuth and UMA tokens.

### Built With

- [Python](https://www.python.org//)
- [PyTest](https://docs.pytest.org)
- [YAML](https://yaml.org/)
- [Travis CI](https://travis-ci.com/)

### Prerequisites

- [Python 3](https://www.python.org//)
- [Pip](https://pip.pypa.io/en/stable/)
- [Requests](https://pypi.org/project/requests/)
- [Pyjwkest](https://pypi.org/project/pyjwkest/)
- [Pycrypto](https://pypi.org/project/pycrypto/)

### Installation

Download the library using pip

```sh
pip install id4eo-scim-client
```

Enable Test Mode in Gluu by following these procedures: [Protection using Test Mode](https://gluu.org/docs/gluu-server/3.1.6/user-management/scim2/#protection-using-test-mode)
Disable Test Mode and Enable UMA by following these procedures: [Protection using UMA](https://gluu.org/docs/gluu-server/3.1.6/user-management/scim2/#protection-using-uma)

## Documentation & Usage

The component documentation can be found at https://eoepca.github.io/um-common-scim-client/.

For example usages, check main.py

## Roadmap

See the [open issues](https://github.com/EOEPCA/um-common-scim-client/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

## Acknowledgements

- README.md is based on [this template](https://github.com/othneildrew/Best-README-Template) by [Othneil Drew](https://github.com/othneildrew).
