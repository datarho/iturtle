import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import { Application, IPlugin } from '@phosphor/application';
import { Widget } from '@phosphor/widgets';
import { MODULE_NAME, MODULE_VERSION } from './version';
import * as widgetExports from './widget';

const EXTENSION_ID = 'iturtle:plugin';

/**
 * The example plugin.
 */
const turtlePlugin: IPlugin<Application<Widget>, void> = {
    id: EXTENSION_ID,
    requires: [IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
} as unknown as IPlugin<Application<Widget>, void>;

export default turtlePlugin;

function activateWidgetExtension(
    app: Application<Widget>,
    registry: IJupyterWidgetRegistry
): void {
    registry.registerWidget({
        name: MODULE_NAME,
        version: MODULE_VERSION,
        exports: widgetExports,
    });
}
