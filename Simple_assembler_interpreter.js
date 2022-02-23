// https://www.codewars.com/kata/58e24788e24ddee28e000053/train/javascript

function simple_assembler(program){
    const isConstant = val => !Number.isNaN(val) && Number.isFinite(Number(val));
    const registers = {};
    let stackPointer = 0;

    while (stackPointer < program.length) {
        const currentInstruction = program[stackPointer].split(' ');
        const code = currentInstruction[0];

        let register;

        switch (code) {
            case 'mov':
                // requires a source and a destination
                const destination = currentInstruction[1];
                const source = currentInstruction[2];

                // source can be a constant or another register
                if (isConstant(source)) {
                    registers[destination] = Number(source);
                } else {
                    registers[destination] = Number(registers[source]);
                }

                stackPointer += 1;
                break;

            case 'inc':
                register = currentInstruction[1];
                registers[register] = registers[register] + 1;
                stackPointer += 1;
                break;

            case 'dec':
                register = currentInstruction[1];
                registers[register] = registers[register] - 1;
                stackPointer += 1;
                break;

            case 'jnz':
                register = currentInstruction[1];
                const step = currentInstruction[2];

                if (registers[register] === 0) {
                    stackPointer += 1;
                } else {
                    stackPointer += Number(step);
                }
                break;
        }

    }

    return registers;
}