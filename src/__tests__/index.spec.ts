import { createTestModel } from './utils';
import { TurtleModel } from '../widget';

describe('Example', () => {
    describe('ExampleModel', () => {
        it('should be created', () => {
            const model = createTestModel(TurtleModel);
            expect(model).toBeInstanceOf(TurtleModel);
            expect(model.get('value')).toEqual('Hello World');
        });

        it('should be created with a value', () => {
            const state = { value: 'Foo Bar!' };
            const model = createTestModel(TurtleModel, state);
            expect(model).toBeInstanceOf(TurtleModel);
            expect(model.get('value')).toEqual('Foo Bar!');
        });
    });
});
