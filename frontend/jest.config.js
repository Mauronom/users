module.exports = {
  testEnvironment: 'jsdom',

  transform: {
    '^.+\\.ts$': 'babel-jest',
    '^.+\\.vue$': '@vue/vue2-jest',
  },

  moduleFileExtensions: ['ts', 'js', 'vue'],

  testMatch: ['**/tests/**/*.test.ts'],

  moduleNameMapper: {
    '^@domain/(.*)$': '<rootDir>/src/domain/$1',
    '^@app/(.*)$': '<rootDir>/src/app/$1',
    '^@infra/(.*)$': '<rootDir>/src/infra/$1',
  },

  modulePathIgnorePatterns: ['dist', 'node_modules'],
}
