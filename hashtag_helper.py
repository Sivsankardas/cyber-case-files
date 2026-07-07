"""
Builds a dynamic hashtag string for a CVE based on the actual affected
vendor/product (parsed from NVD's CPE data), instead of a static tag set.
"""
import re

VENDOR_HASHTAGS = {
    "microsoft": "#Microsoft #Windows",
    "google": "#Google",
    "apple": "#Apple",
    "linux": "#Linux",
    "linux_kernel": "#Linux #Kernel",
    "cisco": "#Cisco",
    "vmware": "#VMware",
    "adobe": "#Adobe",
    "oracle": "#Oracle",
    "sap": "#SAP",
    "wordpress": "#WordPress",
    "fortinet": "#Fortinet",
    "ivanti": "#Ivanti",
    "citrix": "#Citrix",
    "atlassian": "#Atlassian",
    "android": "#Android",
    "openssl": "#OpenSSL",
    "docker": "#Docker",
    "kubernetes": "#Kubernetes",
    "juniper": "#Juniper",
    "sonicwall": "#SonicWall",
    "paloaltonetworks": "#PaloAlto",
    "apache": "#Apache",
    "mozilla": "#Mozilla #Firefox",
    "samsung": "#Samsung",
    "ibm": "#IBM",
    "dell": "#Dell",
    "hp": "#HP",
    "zoom": "#Zoom",
}

def _clean(word: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", word or "").title()

def extract_vendor_product(cve_item: dict):
    """cve_item is the raw NVD 'cve' object (contains 'configurations')."""
    try:
        for config in cve_item.get("configurations", []):
            for node in config.get("nodes", []):
                for match in node.get("cpeMatch", []):
                    criteria = match.get("criteria", "")
                    parts = criteria.split(":")
                    if len(parts) > 4:
                        return parts[3], parts[4]
    except Exception:
        pass
    return None, None

def get_dynamic_hashtags(cve_item: dict, fallback: str = "#CVE #Vulnerability") -> str:
    vendor, product = extract_vendor_product(cve_item)
    if not vendor:
        return fallback
    known = VENDOR_HASHTAGS.get(vendor.lower())
    if known:
        return known
    tags = []
    v, p = _clean(vendor), _clean(product)
    if v:
        tags.append(f"#{v}")
    if p and p.lower() != v.lower():
        tags.append(f"#{p}")
    return " ".join(tags) if tags else fallback
