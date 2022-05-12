import Rete from "rete";
import * as Socket from "../sockets";

import { TimeControl } from "@/node-editor/controls/TimeControl/TimeControl";
import { ZoneControl } from "@/node-editor/controls/ZoneControl/ZoneControl";

export class FluxoComponent extends Rete.Component {
    constructor(){
        super("Fluxo");
    }

    builder(node) {
        
        var out1 = new Rete.Output('num', "Out", Socket.number);

        return node

          
          .addControl(new ZoneControl(this.editor, 'str1'))
          .addControl(new TimeControl(this.editor, 'str'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}