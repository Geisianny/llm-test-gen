Feature: proxy_story_processado

Scenario: Clean up sumaform leftovers on the containerized proxy
    When  I perform a full salt minion cleanup on "proxy"



Scenario: Reboot after clean up
    Tags: ['@transactional_server']
    When  I reboot the "proxy" host through SSH, waiting until it comes back



Scenario: Log in as admin user
    Given  I am authorized for the "Admin" section



Scenario: Bootstrap the proxy host as a salt minion
    When  I follow the left menu "Systems > Bootstrapping"
    Then  I should see a "Bootstrap Minions" text
    When  I enter the hostname of "proxy" as "hostname"
    And  I enter "22" as "port"
    And  I enter "root" as "user"
    And  I enter "linux" as "password"
    And  I select "1-proxy_key" from "activationKeys"
    And  I click on "Bootstrap"
    And  I wait until I see "Bootstrap process initiated." text



Scenario: Reboot the proxy host
    Tags: ['@transactional_server']
    When  I reboot the "proxy" host through SSH, waiting until it comes back



Scenario: Wait until the proxy host appears
    When  I wait until onboarding is completed for "proxy"



Scenario: Upgrade mgrpxy tool
    When  I upgrade "proxy" with the last "mgrpxy" version



Scenario: Reboot after mgrpxy upgrade
    Tags: ['@transactional_server']
    When  I reboot the "proxy" minion through the web UI



Scenario: Generate containerized proxy configuration
    When  I generate the configuration "/tmp/proxy_container_config.tar.gz" of containerized proxy on the server
    And  I copy the configuration "/tmp/proxy_container_config.tar.gz" of containerized proxy from the server to the proxy



Scenario: Set up the containerized proxy service to support Avahi
    When  I add avahi hosts in containerized proxy configuration



Scenario: Run a containerized proxy
    When  I run "mgrpxy install podman /tmp/proxy_container_config.tar.gz" on "proxy"



Scenario: Wait until containerized proxy service is active
    And  I wait until "uyuni-proxy-pod" service is active on "proxy"
    And  I wait until "uyuni-proxy-httpd" service is active on "proxy"
    And  I wait until "uyuni-proxy-salt-broker" service is active on "proxy"
    And  I wait until "uyuni-proxy-squid" service is active on "proxy"
    And  I wait until "uyuni-proxy-ssh" service is active on "proxy"
    And  I wait until "uyuni-proxy-tftpd" service is active on "proxy"
    And  I wait until port "8022" is listening on "proxy" container
    And  I wait until port "80" is listening on "proxy" container
    And  I wait until port "443" is listening on "proxy" container
    And  I visit "Proxy" endpoint of this "proxy"



Scenario: The containerized proxy should be registered automatically
    When  I follow the left menu "Systems"
    And  I wait until I see the name of "proxy", refreshing the page


