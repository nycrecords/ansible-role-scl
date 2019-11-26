import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.fixture(scope="module")
def enabled_repos(host):
    with host.sudo():
        stdout = host.check_output("subscription-manager repos --list-enabled")

    enabled_repos = []
    for line in stdout.splitlines():
        if line.lower().startswith("repo id:"):
            enabled_repos.append(line.split()[-1])
    return enabled_repos


@pytest.fixture(scope="session")
def expected_repos():
    return (
        "rhel-7-server-rpms",
        "rhel-7-server-extras-rpms",
        "rhel-7-server-optional-rpms",
        "rhel-server-rhscl-7-rpms",
    )


def test_rhsm_subscription_current(host):
    cmd = host.run("sudo subscription-manager status")

    assert "Overall Status: Current" in cmd.stdout


def test_repos_enabled(expected_repos, enabled_repos):
    assert set(expected_repos) == set(enabled_repos)
