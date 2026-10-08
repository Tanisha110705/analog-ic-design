#!/usr/bin/env python3
"""Crop the evidence images in this repository from the original report screenshots.

Provenance record: each committed screenshot is a crop of an image embedded
in one of the course reports (R2, R3, R6; see docs/evidence-audit.md).
The crop boxes keep only the schematic canvas or the plot window, which
removes title bars, file-browser paths, server names, user IDs and status
lines. Pixels inside the box are not modified.

The source PDFs are not part of the repository. To re-run, extract the
embedded images first, e.g.:

    pdfimages -png -p R2.pdf <dir>/img_r2/i
    pdfimages -png -p R3.pdf <dir>/img_r3/i
    pdfimages -png -p R6.pdf <dir>/img_r6/i

then:

    python3 tools/crop_evidence.py <dir> .
"""
import os, sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
C = {
 # (source image, box l,t,r,b, dest)
 'device-characterization/nmos-gm-id/cs-gmid-and-id-vs-vgs.png': ('img_r2/i-006-008.png',(402,123,1276,689)),
 'device-characterization/nmos-gm-id/cs-id-per-w-vs-gmid.png': ('img_r2/i-007-009.png',(442,450,920,758)),
 'amplifiers/common-source/cs-ac-current-and-dc-transfer.png': ('img_r2/i-008-012.png',(3,123,1276,690)),
 'amplifiers/common-source/cs-spectre-pz-log.png': ('img_r2/i-008-011.png',(0,72,1395,712)),
 'amplifiers/common-source/cs-schematic.png': ('img_r2/i-005-006.png',(330,140,1180,620)),
 'device-characterization/nmos-gm-id/mirror-id-vs-vgs.png': ('img_r2/i-016-024.png',(3,123,1276,690)),
 'device-characterization/nmos-gm-id/mirror-gmid-and-id-vs-vgs.png': ('img_r2/i-017-025.png',(165,123,1276,689)),
 'device-characterization/nmos-gm-id/mirror-id-per-w-vs-gmid.png': ('img_r2/i-017-026.png',(165,409,718,689)),
 'current-mirrors/simple/simple-mirror-iout-vs-vout.png': ('img_r2/i-018-027.png',(3,123,1276,689)),
 'current-mirrors/cascode/cascode-mirror-iout-vs-vout.png': ('img_r2/i-018-028.png',(3,123,1276,689)),
 'current-mirrors/simple/simple-mirror-100uA-schematic.png': ('img_r2/i-014-020.png',(280,140,1060,560)),
 'current-mirrors/simple/simple-mirror-500uA-schematic.png': ('img_r2/i-015-021.png',(280,140,1060,560)),
 'current-mirrors/cascode/cascode-mirror-100uA-schematic.png': ('img_r2/i-015-022.png',(280,150,1060,600)),
 'device-characterization/pmos/pmos-testbench-schematic.png': ('img_r3/i-002-001.png',(300,170,1300,700)),
 'device-characterization/pmos/01-id-vs-vgs.png': ('img_r3/i-004-005.png',(3,105,906,486)),
 'device-characterization/pmos/01b-id-vs-vgs-vds-sweep.png': ('img_r3/i-004-006.png',(3,105,905,484)),
 'device-characterization/pmos/02-id-vs-vds-vgs-sweep.png': ('img_r3/i-005-007.png',(3,103,898,482)),
 'device-characterization/pmos/02b-id-vs-vds.png': ('img_r3/i-005-008.png',(3,106,933,492)),
 'device-characterization/pmos/03-gm-vs-vgs.png': ('img_r3/i-005-009.png',(341,121,1022,547)),
 'device-characterization/pmos/04-cgs-vs-vgs.png': ('img_r3/i-006-010.png',(317,116,950,509)),
 'device-characterization/pmos/05-vdsat-vs-vgs.png': ('img_r3/i-006-011.png',(319,117,955,512)),
 'device-characterization/pmos/06-id-per-w-vs-gmid.png': ('img_r3/i-006-012.png',(250,132,963,516)),
 'device-characterization/pmos/07-vth-vs-vgs.png': ('img_r3/i-007-013.png',(292,119,1002,537)),
 'device-characterization/pmos/08-gmid-vs-vgs.png': ('img_r3/i-007-014.png',(331,120,990,530)),
 'device-characterization/pmos/09-ft-vs-gmid.png': ('img_r3/i-007-015.png',(244,136,999,535)),
 'amplifiers/cascode/cascode-sizing-testbench.png': ('img_r3/i-009-017.png',(240,105,1000,500)),
 'amplifiers/cascode/cascode-amplifier-schematic.png': ('img_r3/i-009-018.png',(230,95,850,530)),
 'amplifiers/cascode/cascode-gmid-vs-vgs.png': ('img_r3/i-012-023.png',(210,92,957,517)),
 'amplifiers/cascode/cascode-id-per-w-vs-vgs.png': ('img_r3/i-012-024.png',(0,92,956,515)),
 'amplifiers/cascode/cascode-ac-response.png': ('img_r3/i-012-025.png',(0,92,956,515)),
 'amplifiers/active-load/nmos-testbench.png': ('img_r6/i-008-014.png',(250,120,800,520)),
 'amplifiers/active-load/nmos-gmid-vs-vgs.png': ('img_r6/i-008-015.png',(363,115,1186,640)),
 'amplifiers/active-load/nmos-id-per-w-vs-gmid.png': ('img_r6/i-009-016.png',(352,115,1189,642)),
 'amplifiers/active-load/nmos-id-vs-vgs.png': ('img_r6/i-009-017.png',(3,128,1100,600)),
 'amplifiers/active-load/pmos-testbench.png': ('img_r6/i-009-018.png',(280,150,820,560)),
 'amplifiers/active-load/pmos-id-per-w-vs-gmid.png': ('img_r6/i-010-019.png',(145,130,1103,603)),
 'amplifiers/active-load/pmos-id-vs-vgs.png': ('img_r6/i-010-020.png',(250,150,1146,621)),
 'amplifiers/active-load/pmos-gmid-vs-vgs.png': ('img_r6/i-010-021.png',(313,135,1150,628)),
}
for d,(s,b) in C.items():
    out=os.path.join(dst,d); os.makedirs(os.path.dirname(out),exist_ok=True)
    im=Image.open(os.path.join(src,s)).convert('RGB')
    l,t,r,bt=b; r=min(r,im.width); bt=min(bt,im.height)
    im.crop((l,t,r,bt)).save(out,optimize=True)
    print(d, im.crop((l,t,r,bt)).size)
