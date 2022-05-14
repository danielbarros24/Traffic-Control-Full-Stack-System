import Rete from "rete";
import * as Socket from "../sockets";

import { ZoneControl } from "../controls/ZoneControl/ZoneControl";

export class ZoneComponent extends Rete.Component {
    constructor(){
        super("Zone");
    }

    builder(node) {

        var out1 = new Rete.Output('num', "Out", Socket.road);
        return node
          .addControl(new ZoneControl(this.editor, 'num'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}