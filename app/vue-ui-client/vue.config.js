module.exports = {

    devServer: {
      proxy: {
        '/heartrate': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/spo2': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/temperature': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/position': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/location': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/br': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      },
    },
  };