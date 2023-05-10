import { createTestModel } from './utils';
import { TurtleModel } from '../widget';

describe('turtle', () => {
    describe('turtle model', () => {
        it('should be created with a value', () => {
            const state = { x: 200, y: 300, background: 'white' };
            const model = createTestModel(TurtleModel, state);

            expect(model).toBeInstanceOf(TurtleModel);

            expect(model.get('x')).toEqual(200);
            expect(model.get('y')).toEqual(300);
            expect(model.get('background')).toEqual('white');
        });
    });
});
