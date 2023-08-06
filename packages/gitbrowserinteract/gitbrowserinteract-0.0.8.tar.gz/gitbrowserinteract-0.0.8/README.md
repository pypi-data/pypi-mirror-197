# Automatically get and set GitHub & GitLab personal access tokens/ssh deploy keys

Horrible boiler plate to automate 2 tasks in GitHub, and 1 in GitLab:

1. Set an ssh deploy key in your GitHub account, such that you can push the
   GitLab build status icons to a specific (hardcoded) repository in your GitHub
   account.
1. Generate and get/export a GitHub personal access token, such that you can
   set the commit statuses of your GitHub commits. (This is used to display the
   GitLab CI results in your GitHub repository pull requests).
1. Get a GitLab runner token in your own GitLab server. (I did not yet find
   out how to do that through docker itself using bash only).

## Usage: do once

Download/clone this repository.

1. If you don't have pip: open Anaconda prompt and browse to the directory of
   this readme:

```
cd /home/<your path to the repository folder>/
```

1. To use this package, first make a new conda environment and activate (it
   this automatically installs everything you need).

```
conda env create --file environment.yml
```

## Usage: do every time you start Anaconda

1. Activate the conda environment you created:

```
conda activate get_gitlab_generation_token
```

## Usage: do every run (Set ssh-deploy key in GitHub for pushing build status icons)

```
python -m gitbrowserinteract --d --ssh <the public ssh key that was created>
```

- The `--d` indicates you are setting the deploy ssh key in GitHub.
- The `-ssh <some ssh key>` is used to absorb/take in the public ssh key that
  you want to add to github.

## Usage: do every run

Create and get GitHub personal access token for setting commit build statuses

```
python -m gitbrowserinteract -hubcpat
```

- The `--hubcpat` indicates you are letting GitHub create a personal access
  token and storing it.

More complete:

```sh
cd $repo_name && conda deactivate && conda activate get_gitlab_generation_token \
&& python -m gitbrowserinteract --hubcpat -hu $github_username -hp $github_pwd
cd $repo_name && conda deactivate && conda activate get_gitlab_generation_token \
&& python -m gitbrowserinteract --d -hu $github_username -hp $github_pwd
```

## Usage: do every run (Create and get GitLab runnertoken)

```
python -m gitbrowserinteract --g
```

or, to run it from bash as a pip package:

```bash
python -m gitbrowserinteract.__main__ --glr
```

- The `--g` indicates you are letting GitLab generate a personal access token
  and storing it.

## Testing

1. Testing is as simple as running the following command in the root directory
   of this repository in Anaconda prompt:

```
python -m pytest
```

from the root directory of this project.

<!-- Un-wrapped URL's below (Mostly for Badges) -->

## Updating

Build the pip package with:

```
pip install --upgrade pip setuptools wheel
# pip install "keyring>=23.11"
pip install twine
```

Install the pip package locally with:

```
pip install -e .
```

Upload the pip package to the world with:

```
rm -r dist
rm -r build
python3 setup.py sdist bdist_wheel
python -m twine upload dist/\*
```
