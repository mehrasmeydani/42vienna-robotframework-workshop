*** Settings ***
Documentation     Convenience resource that imports all page-level resources.
...               Import this single file to get access to all SauceDemo keywords.
Resource          common.resource
Resource          login_page.resource
Resource          products_page.resource
Resource          cart_page.resource
Resource          checkout_page.resource
Resource		  product_list.resource
