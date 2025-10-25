import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    # Asumiendo que el body viene como un string JSON
    try:
        body = json.loads(event.get('body', '{}'))
        if not body:
             raise ValueError("Cuerpo de solicitud vacío")
        
        tenant_id = body['tenant_id']
        alumno_id = body['alumno_id']
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error en parámetros de entrada: {str(e)}')
        }

    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        item = response.get('Item')
        
        if item:
            # Alumno encontrado
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            # Alumno no encontrado
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Alumno no encontrado'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error interno del servidor: {str(e)}')
        }
