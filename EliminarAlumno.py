import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    try:
        # --- CORRECCIÓN ---
        body = event.get('body')
        if not body:
             raise ValueError("Cuerpo de solicitud vacío")
        
        tenant_id = body['tenant_id']
        alumno_id = body['alumno_id']
        
    except (KeyError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error en parámetros de entrada: {str(e)}')
        }

    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        
        response = table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            ReturnValues='ALL_OLD'
        )
        
        if 'Attributes' in response:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Alumno eliminado exitosamente',
                    'item_eliminado': response['Attributes']
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Alumno no encontrado, no se eliminó nada'})
            }
            
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error de DynamoDB: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error interno del servidor: {str(e)}')
        }
