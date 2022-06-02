import Rete from "rete";
import * as Socket from "../sockets";

import { TimeControl } from '@/node-editor/controls/TimeControl/TimeControl'

export class DurationComponent extends Rete.Component {
    constructor(){
        super("Duration (s)");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.constant);
        return node

          .addControl(new TimeControl(this.editor, 'str'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.str;
    }

    toJsonLogic(node) {
        return node.data.str;
    }
}