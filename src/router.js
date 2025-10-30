const { URL } = require('url');

class Router {
  constructor() {
    this.routes = [];
  }

  register(method, path, handler) {
    const { regex, keys } = this.compile(path);
    this.routes.push({ method: method.toUpperCase(), regex, keys, handler });
  }

  compile(path) {
    const segments = path.split('/').filter(Boolean);
    const keys = [];
    const pattern = segments
      .map((segment) => {
        if (segment.startsWith(':')) {
          keys.push(segment.slice(1));
          return '([^/]+)';
        }
        return segment.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      })
      .join('/');
    const regex = new RegExp(`^/${pattern}/?$`);
    return { regex, keys };
  }

  async handle(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const route = this.routes.find((candidate) => candidate.method === req.method && candidate.regex.test(url.pathname));
    if (!route) {
      return false;
    }
    const match = url.pathname.match(route.regex);
    const params = {};
    route.keys.forEach((key, index) => {
      params[key] = decodeURIComponent(match[index + 1]);
    });
    const body = await this.parseBody(req);
    try {
      await route.handler({
        req,
        res,
        params,
        query: Object.fromEntries(url.searchParams.entries()),
        body,
        json: (statusCode, payload) => this.sendJson(res, statusCode, payload)
      });
    } catch (error) {
      this.sendError(res, error);
    }
    return true;
  }

  async parseBody(req) {
    if (!['POST', 'PUT', 'PATCH'].includes(req.method)) {
      return null;
    }
    const chunks = [];
    for await (const chunk of req) {
      chunks.push(chunk);
    }
    if (!chunks.length) {
      return null;
    }
    const raw = Buffer.concat(chunks).toString('utf-8');
    if (!raw) {
      return null;
    }
    try {
      return JSON.parse(raw);
    } catch (error) {
      const parsingError = new Error('Não foi possível interpretar o JSON enviado.');
      parsingError.status = 400;
      throw parsingError;
    }
  }

  sendJson(res, statusCode, payload) {
    const body = JSON.stringify(payload);
    res.statusCode = statusCode;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Content-Length', Buffer.byteLength(body));
    res.end(body);
  }

  sendError(res, error) {
    const statusCode = error.status || 500;
    const payload = {
      error: {
        message: error.message || 'Erro interno inesperado.',
        status: statusCode
      }
    };
    this.sendJson(res, statusCode, payload);
  }
}

module.exports = Router;
