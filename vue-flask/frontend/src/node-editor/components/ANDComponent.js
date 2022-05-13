import Rete from "rete";
import * as Socket from "../sockets";

export class ANDComponent extends Rete.Component {
    constructor(){
        super("AND");
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In", Socket.boolean, true);
        var out = new Rete.Output('num', "Out", Socket.boolean);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const { inputs } = node;
        
        const inputNum = inputs.get('num1');
        const { connections } = inputNum;

        return {
            "and": connections.map(connection => {
                const connectionNode = connection.output.node;
                const connectionComponent = this.editor.getComponent(connectionNode.name);
                return connectionComponent.toJsonLogic?.(connectionNode)
            })  
        }  
    }
}