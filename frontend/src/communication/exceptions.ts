export abstract class APIError extends Error {
    private data: any;

    protected constructor(message: string, data: any) {
        super(message)
        this.name = "APIError"
        this.data = data
    }
}

export class BadRequestError extends APIError {
    public constructor(message: string, data: any) {
        super(message, data);
        this.name = "BadRequestError"
    }
}

export class UnauthorizedError extends APIError {
    public constructor(message: string, data: any) {
        super(message, data);
        this.name = "UnauthorizedError"
    }
}

export class PermissionDeniedError extends APIError {
    public constructor(message: string, data: any) {
        super(message, data);
        this.name = "PermissionDeniedError"
    }
}

export class NotFoundError extends APIError {
    public constructor(message: string, data: any) {
        super(message, data);
        this.name = "NotFoundError"
    }
}

export class ServerError extends APIError {
    public constructor(message: string, data: any) {
        super(message, data);
        this.name = "ServerError"
    }
}

