import ConnectionPlugin from "rete-connection-plugin";
import VueRenderPlugin from "rete-vue-render-plugin";
import ContextMenuPlugin from "rete-context-menu-plugin";
import AreaPlugin from "rete-area-plugin";
import KeyboardPlugin from 'rete-keyboard-plugin';

import router from '@/router'
import vuetify from '@/plugins/vuetify'

import { AddComponent }      from '@/node-editor/components/arithmetic-operators/AddComponent'
import { SubComponent }      from '@/node-editor/components/arithmetic-operators/SubComponent'
import { MultiplyComponent } from '@/node-editor/components/arithmetic-operators/MultiplyComponent'
import { DivisionComponent } from '@/node-editor/components/arithmetic-operators/DivisionComponent'
import { MaxComponent }      from '@/node-editor/components/arithmetic-operators/MaxComponent'
import { MinComponent }      from '@/node-editor/components/arithmetic-operators/MinComponent'

import { ANDComponent }                  from '@/node-editor/components/logical-operators/ANDComponent'
import { ORComponent }                   from '@/node-editor/components/logical-operators/ORComponent'
import { NOTComponent }                  from '@/node-editor/components/logical-operators/NOTComponent'
import { DifferentThanComponent }        from '@/node-editor/components/logical-operators/DifferentThanComponent'
import { EqualToComponent }              from '@/node-editor/components/logical-operators/EqualToComponent'
import { GreaterThanComponent }          from '@/node-editor/components/logical-operators/GreaterThanComponent'
import { GreaterThanOrEqualToComponent } from '@/node-editor/components/logical-operators/GreaterThanOrEqualToComponent'
import { LessThanComponent }             from '@/node-editor/components/logical-operators/LessThanComponent'
import { LessThanOrEqualToComponent }    from '@/node-editor/components/logical-operators/LessThanOrEqualToComponent'

import { ConstantComponent }         from '@/node-editor/components/variables/ConstantComponent'
import { DurationComponent }         from '@/node-editor/components/variables/DurationComponent'
import { JamComponent }              from '@/node-editor/components/variables/JamComponent'
import { FlowComponent }             from '@/node-editor/components/variables/FlowComponent'
import { CrowdDetectionComponent }   from '@/node-editor/components/variables/CrowdDetectionComponent'
import { DoubleParkComponent }       from '@/node-editor/components/variables/DoubleParkComponent'
import { StayTimeComponent }         from '@/node-editor/components/variables/StayTimeComponent'
import { VehicleDetectionComponent } from '@/node-editor/components/variables/VehicleDetectionComponent'
import { VehicleNumberComponent } from '@/node-editor/components/variables/VehicleNumberComponent'

import { GpioComponent } from '@/node-editor/components/GpioComponent'

import Rete from "rete";


export default async function(container) {
    const components = [new GpioComponent(), new VehicleDetectionComponent(), new VehicleNumberComponent, new StayTimeComponent(), new FlowComponent(), new DoubleParkComponent(),
        new JamComponent(), new CrowdDetectionComponent(), new DurationComponent(), new ConstantComponent(), new AddComponent(), new SubComponent(), 
        new MultiplyComponent(), new DivisionComponent(), new MaxComponent(), new MinComponent(), new EqualToComponent(), new DifferentThanComponent(), 
        new GreaterThanComponent(), new LessThanComponent(), new GreaterThanOrEqualToComponent(), new LessThanOrEqualToComponent(), 
        new ANDComponent(), new ORComponent(), new NOTComponent()];
  
    const editor = new Rete.NodeEditor("demo@0.1.0", container);

    editor.use(ConnectionPlugin);
    editor.use(VueRenderPlugin, {
        options: {
          router,
          vuetify
        }
    });
    editor.use(ContextMenuPlugin);
    editor.use(AreaPlugin);
    editor.use(KeyboardPlugin);
  
    const engine = new Rete.Engine("demo@0.1.0");
  
    components.map(c => {
      editor.register(c);
      engine.register(c);
    });

    var n1 = await components[0].createNode({num: 2});
    var n2 = await components[0].createNode({num: 0});
    var add = await components[1].createNode();
    
    n1.position = [80, 200];
    n2.position = [80, 400];
    add.position = [500, 240];
  
    editor.on(
      "process nodecreated noderemoved connectioncreated connectionremoved",
      async () => {
        await engine.abort();
        await engine.process(editor.toJSON());
      }
    );
  
    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');

    return {
      editor
    }
  }
  
