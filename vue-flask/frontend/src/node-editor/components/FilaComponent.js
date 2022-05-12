import Rete from "rete";
import * as Socket from "../sockets";

import { ZoneControl } from "@/node-editor/controls/ZoneControl/ZoneControl"


export class FilaComponent extends Rete.Component {
    constructor(){
        super("Fila");
    }

    builder(node) {

        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node

          .addInput(inp1)
          .addControl(new ZoneControl(this.editor, 'num'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}