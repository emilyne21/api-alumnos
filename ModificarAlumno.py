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
        alumno_datos = body['alumno_datos']
        
    except (KeyError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error en parámetros de entrada: {str(e)}')
        }

    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')

        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression="SET alumno_datos = :datos",
            ExpressionAttributeValues={
                ':datos': alumno_datos
            },
            ConditionExpression="attribute_exists(tenant_id) AND attribute_exists(alumno_id)",
            ReturnValues="UPDATED_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Alumno modificado exitosamente',
                'updated_attributes': response.get('Attributes')
            })
        }
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Alumno no encontrado, no se puede modificar'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error de DynamoDB: {str(e)}')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error interno del servidor: {str(e)}')
        }
