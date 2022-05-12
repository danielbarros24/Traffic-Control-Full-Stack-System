import Rete from "rete";
import VueVehicleTypeControl from "./VehicleTypeControl.vue";

export class VehicleTypeControl extends Rete.Control {
  constructor(emitter, key, readonly) {
    super(key);
    this.component = VueVehicleTypeControl;
    this.props = { emitter, ikey: key, readonly };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}