module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(ts|js)$': 'babel-jest',
  //  '^.+\\.vue$': '@vue/vue2-jest',
  },
  moduleFileExtensions: ['ts', 'js', 'vue'],
  testMatch: ['**/*.test.ts'],
  modulePathIgnorePatterns: ['dist', 'node_modules'],
}
