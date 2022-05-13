import Rete from "rete";
import * as Socket from "../sockets";

import { NumControl } from '@/node-editor/controls/NumControl/NumControl'

export class TimeComponent extends Rete.Component {
    constructor(){
        super("Tempo (s)");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.number);
        return node
          .addControl(new NumControl(this.editor, 'num'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}