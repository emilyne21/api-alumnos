import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    try:
        # --- CORRECCIÓN ---
        # event['body'] YA es un diccionario, no necesitamos json.loads()
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
        
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        item = response.get('Item')
        
        if item:
            # Alumno encontrado
            # API Gateway espera un 'body' que sea un string JSON
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
