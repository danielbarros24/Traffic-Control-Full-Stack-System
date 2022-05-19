import Rete from "rete";
import * as Socket from "../sockets";

import { TimeControl } from "@/node-editor/controls/TimeControl/TimeControl";
import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";

export class FlowComponent extends Rete.Component {
    constructor(){
        super("Flow");
    }

    builder(node) {
        
        var out1 = new Rete.Output('num', "Out", Socket.number);

        return node

          .addControl(new SelectControl(this.editor, 'type1', [
              { text: 'Sensor 1 - Route 1', value: 'T1-1' },
              { text: 'Sensor 1 - Route 2', value: 'T1-2' }
          ], "Zone"))
          .addControl(new TimeControl(this.editor, 'str'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
    toJsonLogic(node) {
        const zone = node.data.type1;
        const duration = node.data.str;

        return {
            "flow": [ zone, duration ]
        }  
    }
}