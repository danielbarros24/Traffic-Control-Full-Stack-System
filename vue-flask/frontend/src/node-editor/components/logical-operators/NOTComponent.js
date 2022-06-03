import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/logical-operators/Node.vue";

export class NOTComponent extends Rete.Component {
    constructor(){
        super("NOT");
        this.data.component = Node;
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In", Socket.boolean);
        var out = new Rete.Output('num', "Out", Socket.boolean);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }
}