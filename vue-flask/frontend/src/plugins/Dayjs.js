import Vue from 'vue';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import dayjsPluginUTC from 'dayjs-plugin-utc'

dayjs.extend(relativeTime);
dayjs.extend(dayjsPluginUTC)

Object.defineProperties(Vue.prototype, {
    $date: {
        get() {
            return dayjs
        }
    }
});