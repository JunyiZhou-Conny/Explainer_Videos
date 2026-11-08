# Makes the edited copies the checks run, from the unchanged files in /w (copies of 5950118).
# Usage: python3 edit.py <what>. Prints the changed lines it wrote.
import re, sys
what = sys.argv[1]
def rd(p): return open(p).read().split("\n")
def wr(p, L): open(p, "w").write("\n".join(L))
if what == "warnbook":         # deploy-provision-instance.yml:54-57 as a localhost play
    L = rd("/w/deploy-provision-instance.yml")[53:57]
    head = ["- name: deploy-provision-instance.yml lines 54-57, run on localhost",
            "  hosts: localhost", "  connection: local", "  gather_facts: false", "  tasks:"]
    wr("/w/warnbook.yml", head + L + [""])
    print("\n".join(head + L))
elif what == "toggle":           # README:107-111: line 4 commented, line 7 active (as laptop/45)
    L = rd("/w/inventory.yml")
    L[3] = "    # " + L[3].lstrip(); L[6] = L[6].replace("    # ansible_ssh", "    ansible_ssh", 1)
    wr("/w/inventory-local.yml", L); print("\n".join(L[3:7]))
elif what == "gate":             # B5 step 1: `when:` on "Create EC2 instance"
    L = rd("/w/deploy-create-instance.yml")
    assert L[60].strip() == "register: instance", L[60]
    L.insert(61, '      when: cluster_state == "present"')
    wr("/w/create-gated.yml", L); print("\n".join(L[58:63]))
elif what == "fixed":            # B5 step 2: the four tasks of teardown-fixed.yml replace lines 94-100
    L = rd("/w/create-gated.yml")
    i = L.index("    - name: Remove EBS volume")
    assert L[i-1].strip().startswith("# Replace GCP disk removal"), L[i-1]
    new = [l for l in open("/checks/teardown-fixed.yml").read().split("\n") if not l.startswith("#")]
    L[i-1:i+6] = new
    wr("/w/create-fixed.yml", L); print("".join("%3d %s\n" % (n+1, l) for n, l in enumerate(L) if n >= i-2 and n < i+len(new)))
