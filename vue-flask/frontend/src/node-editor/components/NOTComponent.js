import Rete from "rete";
import * as Socket from "../sockets";


export class NOTComponent extends Rete.Component {
    constructor(){
        super("NOT");
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