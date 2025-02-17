# dOVHer
Small utility app to update DynDNS records at OVH account

I wrote it for myself, to keep my custom domain updated and pointing out to dynamic IP address. I automated it up to be launched with every IP change.

Application reads current IP address, and sets it as A or AAA (based on config) record value in OVH DNS servers.

In order to make it work, you need OVH credentials, full description hot to get them [here](https://certbot-dns-ovh.readthedocs.io/en/stable/).

## Configuration

Copy or rename `config_example.json` to `config.json`, fill necessary data.

```json
{
  "DEBUG": "True", // enable debugging
  "DEVELOPMENT": "True", // development mode - DRY RUN (no changes in OVH)
  "OVH_ENDPOINT": "ovh-eu", // OVH region
  "OVH_APPLICATION_KEY": "application_key", // application key
  "OVH_APPLICATION_SECRET": "application_secret", // application secret
  "OVH_CONSUMER_KEY": "consumer_key", // consumer key
  "LANGUAGE": "en", // language for messages
  "HOSTS": [ // lists of records to be updated with current IP address
    {
      "type": "A",
      "domain": "example.com",
      "subdomain": "www"
    },
    {
      "type": "A",
      "domain": "example.com",
      "subdomain": "test"
    },
    {
      "type": "A",
      "domain": "domain.com",
      "subdomain": "*"
    }
  ]
}
```

## Docker

In order to make the application work correctly, it must be run on machine, which IP address will be source for changes.

You can run application by executing command:

`docker compose up -d`

It will build an image and run it.

## Translations

For now, all few messages are provided in English and Polish.