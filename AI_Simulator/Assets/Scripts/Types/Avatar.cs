using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Avatar : ObjectInfo
{
    public const int maxViewDistance = 10;

    float moveSpeed = 1.5f;
    float moveArcHeight = .2f;

    // State:
    [Header("State")]
    public float hunger;

    // Move data:
    bool animatingMovement;
    Coord moveFromCoord;
    Coord moveTargetCoord;
    Vector3 moveStartPos;
    Vector3 moveTargetPos;
    float moveTime;
    float moveSpeedFactor;
    float moveArcHeightFactor;

    float timeToDeathByHunger = 200f;

    // Other
    const float sqrtTwo = 1.4142f;
    const float oneOverSqrtTwo = 1 / sqrtTwo;

    protected virtual void Update ()
    {
        hunger += Time.deltaTime * 1 / timeToDeathByHunger;

        if (hunger >= 1)
        {
            Die(CauseOfDeath.Hunger);
        }
    }

    void SendSurroundings()
    {
        Environment.UpdateWorldMap();
        string[,] tmpWorldMap = Environment.worldMap;
        string surroundingsMapAscii = "";

        for (int y = 0; y < 9; y++)
        {
            surroundingsMapAscii += "\n";

            for (int x = 0; x < 9; x++)
            {
                int newX = this.coord.x + x;
                int newY = this.coord.y + y;

                surroundingsMapAscii += tmpWorldMap[newX, newY];
            }
        }
        Debug.Log(surroundingsMapAscii);
    }

    void Move(Coord direction)
    {
        StartCoroutine(MoveAvatar(direction));
    }

    IEnumerator MoveAvatar(Coord direction)
    {
        StartMoveToCoord(direction + this.coord);

        while (animatingMovement)
        {
            AnimateMove();
            yield return null;
        }
    }

    void SayHello()
    {
        var oneUp = Coord.up + coord;
        Debug.Log(oneUp);
    }

    protected void StartMoveToCoord(Coord target)
    {
        moveFromCoord = coord;
        moveTargetCoord = target;
        moveStartPos = transform.position;
        moveTargetPos = Environment.tileCentres[moveTargetCoord.x, moveTargetCoord.y];
        animatingMovement = true;

        bool diagonalMove = Coord.SqrDistance(moveFromCoord, moveTargetCoord) > 1;
        moveArcHeightFactor = (diagonalMove) ? sqrtTwo : 1;
        moveSpeedFactor = (diagonalMove) ? oneOverSqrtTwo : 1;

        LookAt(moveTargetCoord);
    }

    protected void LookAt(Coord target)
    {
        if (target != coord)
        {
            Coord offset = target - coord;
            transform.eulerAngles = Vector3.up * Mathf.Atan2(offset.x, offset.y) * Mathf.Rad2Deg;
        }
    }

    void AnimateMove()
    {
        // Move in an arc from start to end tile
        moveTime = Mathf.Min(1, moveTime + Time.deltaTime * moveSpeed * moveSpeedFactor);
        float height = (1 - 4 * (moveTime - .5f) * (moveTime - .5f)) * moveArcHeight * moveArcHeightFactor;
        transform.position = Vector3.Lerp(moveStartPos, moveTargetPos, moveTime) + Vector3.up * height;

        // Finished moving
        if (moveTime >= 1)
        {
            Environment.RegisterMove(this, moveFromCoord, moveTargetCoord);
            coord = moveTargetCoord;

            animatingMovement = false;
            moveTime = 0;
        }
    }

}
