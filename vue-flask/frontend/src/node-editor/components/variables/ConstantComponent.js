import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

import { NumControl } from '@/node-editor/controls/NumControl/NumControl'

export class ConstantComponent extends Rete.Component {
    constructor(){
        super("Constant");
        this.data.component = Node;
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.constant);
        return node
          .addControl(new NumControl(this.editor, 'value'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        return node.data.value;
    }
}