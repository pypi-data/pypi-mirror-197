#!/usr/bin/python3

import os
import sys

from saigen.confbase import *
from saigen.confutils import *


class Enis(ConfBase):

    def __init__(self, params={}):
        super().__init__(params)

    def items(self):
        self.num_yields = 0
        print('  Generating %s ...' % os.path.basename(__file__), file=sys.stderr)
        p = self.params

        for eni_index, eni in enumerate(range(p.ENI_START, p.ENI_START + p.ENI_COUNT * p.ENI_STEP, p.ENI_STEP)):
            vm_underlay_dip = str(ipaddress.ip_address(p.PAL) + eni_index * int(ipaddress.ip_address(p.IP_STEP1)))

            
            eni_data = {
                'name': 'eni_#%d' % eni,
                'op': 'create',
                'type': 'SAI_OBJECT_TYPE_ENI',
                'attributes': [
                    'SAI_ENI_ATTR_CPS', '10000',
                    'SAI_ENI_ATTR_PPS', '100000',
                    'SAI_ENI_ATTR_FLOWS', '100000',
                    'SAI_ENI_ATTR_ADMIN_STATE', 'True',
                    'SAI_ENI_ATTR_VM_UNDERLAY_DIP', vm_underlay_dip,
                    'SAI_ENI_ATTR_VM_VNI', '%d' % eni,
                    'SAI_ENI_ATTR_VNET_ID', '$vnet_#eni%d' % eni,
                    'SAI_ENI_ATTR_INBOUND_V4_STAGE1_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V4_STAGE2_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V4_STAGE3_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V4_STAGE4_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V4_STAGE5_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V6_STAGE1_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V6_STAGE2_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V6_STAGE3_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V6_STAGE4_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_INBOUND_V6_STAGE5_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V4_STAGE1_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V4_STAGE2_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V4_STAGE3_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V4_STAGE4_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V4_STAGE5_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V6_STAGE1_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V6_STAGE2_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V6_STAGE3_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V6_STAGE4_DASH_ACL_GROUP_ID', '0',
                    'SAI_ENI_ATTR_OUTBOUND_V6_STAGE5_DASH_ACL_GROUP_ID', '0',
                ]
            }
            for nsg_index in range(1, (p.ACL_NSG_COUNT + 1)):
                stage_index = eni_data['attributes'].index('SAI_ENI_ATTR_INBOUND_V4_STAGE%d_DASH_ACL_GROUP_ID' % nsg_index)
                eni_data['attributes'][stage_index + 1] = '$in_acl_group_#eni%dnsg%d' % (eni, nsg_index)
                stage_index = eni_data['attributes'].index('SAI_ENI_ATTR_OUTBOUND_V4_STAGE%d_DASH_ACL_GROUP_ID' % nsg_index)
                eni_data['attributes'][stage_index + 1] = '$out_acl_group_#eni%dnsg%d' % (eni, nsg_index)

            self.num_yields += 1
            yield eni_data


if __name__ == '__main__':
    conf = Enis()
    common_main(conf)
